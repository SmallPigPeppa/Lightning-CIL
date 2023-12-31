import sys
import logging
import copy
import torch
from utils import factory
from utils.data_manager import DataManager
from utils.toolkit import count_parameters
import os


def train(args):
    seed_list = copy.deepcopy(args["seed"])
    device = copy.deepcopy(args["device"])

    for seed in seed_list:
        args["seed"] = seed
        args["device"] = device
        _train(args)


def _train(args):
    init_cls = 0 if args["init_cls"] == args["increment"] else args["init_cls"]
    # logs_name = "logs/{}/{}/{}/{}".format(args["model_name"],args["dataset"], init_cls, args['increment'])
    #
    # if not os.path.exists(logs_name):
    #     os.makedirs(logs_name)

    logs_name = "logs/{}".format(args["model_name"])

    if not os.path.exists(logs_name):
        os.makedirs(logs_name)

    logfilename = "logs/{}/{}_{}_{}_{}_{}_{}".format(
        args["model_name"],
        args["prefix"],
        args["dataset"],
        init_cls,
        args["increment"],
        args["seed"],
        args["convnet_type"],
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(filename)s] => %(message)s",
        handlers=[
            logging.FileHandler(filename=logfilename + ".log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    _set_random()
    _set_device(args)
    print_args(args)
    data_manager = DataManager(
        args["dataset"],
        args["shuffle"],
        args["seed"],
        args["init_cls"],
        args["increment"],
    )

    model = factory.get_model(args["model_name"], args)
    if 'pretrained_model' in args.keys():
        import warnings
        print(f"load pretrained model from {args['pretrained_model']}")
        ckpt_path = args['pretrained_model']
        state = torch.load(ckpt_path)["state_dict"]
        for k in list(state.keys()):
            if "encoder" in k:
                state[k.replace("encoder", "backbone")] = state[k]
                warnings.warn(
                    "You are using an older checkpoint. Use a new one as some issues might arrise."
                )
            if "backbone" in k:
                state[k.replace("backbone.", "")] = state[k]
            del state[k]

        if args['model_name'] in ['memo']:
            model._network.TaskAgnosticExtractor.load_state_dict(state, strict=False)
            model._network.pretrained_weight = state
        elif args['model_name'] in ['der', 'foster', 'rmm-foster', ]:
            model._network.pretrained_weight = state
        elif args['model_name'] in ['fetril', 'simplecil', 'pass', 'il2a', 'icarl', 'lwf', 'ucir', 'podnet']:
            model._network.convnet.load_state_dict(state, strict=False)
        elif args['model_name'] in ['ssre']:
            for k in list(state.keys()):
                if "downsample" in k:
                    del state[k]
            model._network.convnet.load_state_dict(state, strict=False)
        else:
            pass

    cnn_curve, nme_curve = {"top1": [], "top5": []}, {"top1": [], "top5": []}
    for task in range(data_manager.nb_tasks):
        logging.info("All params: {}".format(count_parameters(model._network)))
        logging.info(
            "Trainable params: {}".format(count_parameters(model._network, True))
        )
        # model.incremental_train(data_manager)
        if args['model_name'] in ['pass', 'il2a'] and len(args["device"]) > 1:
            model = torch.nn.DataParallel(model, args["device"])
            model.module.incremental_train(data_manager)
        else:
            model.incremental_train(data_manager)

        cnn_accy, nme_accy = model.eval_task()
        model.after_task()

        if nme_accy is not None:
            logging.info("CNN: {}".format(cnn_accy["grouped"]))
            logging.info("NME: {}".format(nme_accy["grouped"]))

            cnn_curve["top1"].append(cnn_accy["top1"])
            cnn_curve["top5"].append(cnn_accy["top5"])

            nme_curve["top1"].append(nme_accy["top1"])
            nme_curve["top5"].append(nme_accy["top5"])

            logging.info("CNN top1 curve: {}".format(cnn_curve["top1"]))
            logging.info("CNN top5 curve: {}".format(cnn_curve["top5"]))
            logging.info("NME top1 curve: {}".format(nme_curve["top1"]))
            logging.info("NME top5 curve: {}\n".format(nme_curve["top5"]))

            print('Average Accuracy (CNN):', sum(cnn_curve["top1"]) / len(cnn_curve["top1"]))
            print('Average Accuracy (NME):', sum(nme_curve["top1"]) / len(nme_curve["top1"]))

            logging.info("Average Accuracy (CNN): {}".format(sum(cnn_curve["top1"]) / len(cnn_curve["top1"])))
            logging.info("Average Accuracy (NME): {}".format(sum(nme_curve["top1"]) / len(nme_curve["top1"])))
        else:
            logging.info("No NME accuracy.")
            logging.info("CNN: {}".format(cnn_accy["grouped"]))

            cnn_curve["top1"].append(cnn_accy["top1"])
            cnn_curve["top5"].append(cnn_accy["top5"])

            logging.info("CNN top1 curve: {}".format(cnn_curve["top1"]))
            logging.info("CNN top5 curve: {}\n".format(cnn_curve["top5"]))

            print('Average Accuracy (CNN):', sum(cnn_curve["top1"]) / len(cnn_curve["top1"]))
            logging.info("Average Accuracy (CNN): {}".format(sum(cnn_curve["top1"]) / len(cnn_curve["top1"])))


def _set_device(args):
    device_type = args["device"]
    gpus = []

    for device in device_type:
        if device_type == -1:
            device = torch.device("cpu")
        else:
            device = torch.device("cuda:{}".format(device))

        gpus.append(device)

    args["device"] = gpus


def _set_random():
    torch.manual_seed(1)
    torch.cuda.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def print_args(args):
    for key, value in args.items():
        logging.info("{}: {}".format(key, value))
