import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Store resume in a variable
resume = docx2txt.process("C:/Users/vaisa/Documents/vaisakhCV.docx")

# # print(resume)

job_descriptoin = "React Python (Django, Flask) Android C Programming C++ Programming MySQL SQLite HTML CSS Bootstrap JavaScript jQuery MS Office tools"

# # A list of text
# text = [ resume, job_descriptoin ]

# cv = CountVectorizer()
# count_matrix = cv.fit_transform(text)

# # print the similarity scores
# # print("\nSimilarity Scores:")
# # print(cosine_similarity(count_matrix))

# # get match percentage
# matchPercentage = cosine_similarity(count_matrix)[0][1]*100
# matchPercentage = round(matchPercentage, 2) # round to two decimal places
# print("\nYour resume mathes about " +str(matchPercentage)+"% of the job description")


def matchResume(linkToResume, jobDescription):
    resume = docx2txt.process(linkToResume)
    text = [ resume, jobDescription ]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matchPercentage = cosine_similarity(count_matrix)[0][1]*100
    matchPercentage = round(matchPercentage, 2) 
    return str(matchPercentage)

print(matchResume("C:/Users/vaisa/Documents/vaisakhCV.docx", job_descriptoin))