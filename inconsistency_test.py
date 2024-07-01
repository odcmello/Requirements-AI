import torch 

class inconsistency_test():
        
        def test(self,sentence1,sentence2,predictor, model,device):
            if(sentence1 != '' and sentence2 != ''):
                input = predictor(sentence1, sentence2, truncation=True, return_tensors="pt") 
                output = model(input["input_ids"].to(device))
                prediction = torch.softmax(output[0][0], -1)
                label_names = ["entailment", "neutral", "contradiction"]
                if label_names[prediction.argmax(0).tolist()] == "contradiction":
                    print(sentence1)
                    print(sentence2)
                    return 1
                else:
                    return 0
            else:
                return 0

            


