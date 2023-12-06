#CUDA_VISIBLE_DEVICES=0 python main.py --config=./exps_semi/imagenet100/5steps/fetril.json &
#CUDA_VISIBLE_DEVICES=1 python main.py --config=./exps_semi/imagenet100/10steps/fetril.json
#CUDA_VISIBLE_DEVICES=2 python main.py --config=./exps_semi/imagenet100/5steps/foster.json &
#CUDA_VISIBLE_DEVICES=3 python main.py --config=./exps_semi/imagenet100/10steps/foster.json &
CUDA_VISIBLE_DEVICES=4 python main.py --config=./exps_semi/imagenet100/5steps/memo.json &
#CUDA_VISIBLE_DEVICES=5 python main.py --config=./exps_semi/imagenet100/10steps/memo.json &
#CUDA_VISIBLE_DEVICES=6 python main.py --config=./exps_semi/imagenet100/5steps/rmm-foster.json &
CUDA_VISIBLE_DEVICES=7 python main.py --config=./exps_semi/imagenet100/10steps/rmm-foster.json

#CUDA_VISIBLE_DEVICES=0 python main.py --config=./exps_semi/imagenet100/5steps/simplecil.json &
#CUDA_VISIBLE_DEVICES=1 python main.py --config=./exps_semi/imagenet100/10steps/simplecil.json
#CUDA_VISIBLE_DEVICES=2 python main.py --config=./exps_semi/imagenet100/5steps/ssre.json &
#CUDA_VISIBLE_DEVICES=3 python main.py --config=./exps_semi/imagenet100/10steps/ssre.json

#CUDA_VISIBLE_DEVICES=4 python main.py --config=./exps_semi/imagenet100/5steps/der.json &
#CUDA_VISIBLE_DEVICES=5 python main.py --config=./exps_semi/imagenet100/10steps/der.json &
#CUDA_VISIBLE_DEVICES=6 python main.py --config=./exps_semi/imagenet100/5steps/ucir.json &
#CUDA_VISIBLE_DEVICES=7 python main.py --config=./exps_semi/imagenet100/10steps/ucir.json &
#CUDA_VISIBLE_DEVICES=0 python main.py --config=./exps_semi/imagenet100/5steps/icarl.json &
#CUDA_VISIBLE_DEVICES=1 python main.py --config=./exps_semi/imagenet100/10steps/icarl.json &
#CUDA_VISIBLE_DEVICES=2 python main.py --config=./exps_semi/imagenet100/5steps/lwf.json &
#CUDA_VISIBLE_DEVICES=3 python main.py --config=./exps_semi/imagenet100/10steps/lwf.json &
#CUDA_VISIBLE_DEVICES=4 python main.py --config=./exps_semi/imagenet100/5steps/podnet.json &
#CUDA_VISIBLE_DEVICES=5 python main.py --config=./exps_semi/imagenet100/10steps/podnet.json &
#CUDA_VISIBLE_DEVICES=6 python main.py --config=./exps_semi/imagenet100/5steps/pass.json &
#CUDA_VISIBLE_DEVICES=7 python main.py --config=./exps_semi/imagenet100/10steps/pass.json &