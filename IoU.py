import pickle
from teste import bb_intersection_over_union
from Boxes import Boxes, Box

boxes_true = Boxes(540)
boxes_predicted = Boxes(540)

boxes_true.load("boxes.b")
boxes_predicted.load("boxes_predicted_svm_25.b")


total_score=0

true_positive = 0

false_positive = 0

predicteds = 0
trues = 0

for i in range(len(boxes_predicted.boxes)):
    bxs_p = boxes_predicted.get(i)
    bxs_t = boxes_true.get(i)
    predicteds += len(bxs_p)
    trues += len(bxs_t)
    if(len(bxs_t)>0):
        for bp in bxs_p:
            for bt in bxs_t:
                score = bb_intersection_over_union(bp.box,bt.normalize())
                if(score>0.1):
                    total_score+=score
                    true_positive+=1
    else:
        false_positive+=len(bxs_p)

print("Trues: "+str(trues))
print("Predicted: "+str(predicteds))
print("True positives: "+str(true_positive))
print("False positives: "+str(false_positive))

print("\nAcc: {:.2f}".format(true_positive/predicteds))
print("Prec: {:.2f}".format(true_positive/(true_positive+false_positive)))
print("IoU: {:.2f}%".format(total_score/true_positive*100.0))