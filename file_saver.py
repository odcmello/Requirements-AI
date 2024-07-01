class file_saver():
    def save_file(self,user_stories,detected_c,complete_input,detected_a,ambiguity_input,detected_cs,consistent_input,complete_timer,ambiguity_timer,consistent_timer):
        result = input("Type the test result file name.\n")
        f = open("test_results/" + result + ".txt", "w", encoding='utf-8')

        for i in range(len(user_stories)):
            f.write("User Story: " + user_stories[i] + "\n")
            f.write("Completeness Problems: " + detected_c[i] + "\n")
            f.write("Completeness Test: " + complete_input[i] + "\n")
            f.write("Ambiguity Problems: " + detected_a[i] + "\n")
            f.write("Ambiguity Test: " + ambiguity_input[i] + "\n")
            f.write("Consistency Problems: " + detected_cs[i] + "\n")
            f.write("Consistency Test: " + consistent_input[i] + "\n")
            f.write("Completeness Test Time: " + str(complete_timer[i]) + "\n")
            f.write("Ambiguity Test Time: " + str(ambiguity_timer[i]) + "\n")
            f.write("Consistency Test Time: " + str(consistent_timer[i]) + "\n")
            f.write("\n")
