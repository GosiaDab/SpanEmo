"""
Usage:
    main.py [options]

Options:
    -h --help                         show this screen
    --model-path=<str>                path of the file
    --loss-type=<str>                 Which loss to use cross-ent|corr|joint. [default: ]
    --max-length=<int>                length of sample [default: 128]
    --output-dropout=<float>          prob of dropout applied to output layer [default: 0.1]
    --seed=<int>                      seed [default: 0]
    --test-batch-size=<int>           batch size [default: 32]
    --lang=<str>                      language choice [default: English]
    --test-path=<str>                path of the directory where the file is saved [default: ]
"""
from learner import EvaluateOnTest
from model import SpanEmo
from data_loader import DataClass
from torch.utils.data import DataLoader
import torch
from docopt import docopt
import numpy as np


args = docopt(__doc__)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
if str(device) == 'cuda:0':
    print("Currently using GPU: {}".format(device))
    np.random.seed(int(args['--seed']))
    torch.cuda.manual_seed_all(int(args['--seed']))
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
else:
    print("Currently using CPU")
#####################################################################
# Define Dataloaders
#####################################################################
test_dataset = DataClass(args, args['--test-path'])
test_data_loader = DataLoader(test_dataset,
                              batch_size=int(args['--test-batch-size']),
                              shuffle=False)
print('The number of Test batches: ', len(test_data_loader))
#############################################################################
# Run the model on a Test set
#############################################################################
model = SpanEmo(output_dropout=float(args['--output-dropout']),
                lang=args['--lang'],
                joint_loss=args['--loss-type'],
                alpha=float(args['--alpha-loss']))
learn = EvaluateOnTest(model, test_data_loader, model_path='models/' + args['--model-path'])
learn.predict(device=device)


