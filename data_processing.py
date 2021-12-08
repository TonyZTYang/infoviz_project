# %% [markdown]
# Link for Spring 2022 CS courses: https://schedge.a1liu.com/current/sp/SHU/CSCI?full=true
# Link format for schedule scraping:
#     https://schedge.a1liu.com/{year}/{semester}/generateSchedule?registrationNumbers={regNumber}

# %%
import json
import requests
import re

# links
link_cssp22 = "https://schedge.a1liu.com/current/sp/SHU/CSCI?full=true"
link_csfa21 = "https://schedge.a1liu.com/current/fa/SHU/CSCI?full=true"
link_math = "https://schedge.a1liu.com/current/fa/SHU/MATH?full=true"
# year, semester, regNumber = "2022", "sp", None
# link_schedule = f"https://schedge.a1liu.com/{year}/{semester}/generateSchedule?registrationNumbers={regNumber}"

# files
cs22sp_res = 'data/responses/cs22sp_res.json'
cs21fa_res = 'data/responses/cs22fa_res.json'
cs22sp_cleaned = 'data/processed/cs22sp_cleaned.json'
cs_orgranized = 'data/processed/cs_orgranized.json'
cs_cleaned = 'data/processed/cs_cleaned.json'
links = 'data/processed/links.json'


# %%
# fetch data from api
def fetch_and_save(link, file):
    res = requests.get(link)
    with open(file, 'w') as f:
        json.dump(res.json(), f, indent=True)
    # print info abt the response
    # print("Number of Courses:" + str(len(res.json())))
    # print("Courses:")
    # for i in res.json():
    #     print(i["subjectCode"]["code"] + '-' + i["subjectCode"]["school"] + '-'+ i["deptCourseId"] + '-'+  i["name"])

# %%
fetch_and_save(link_csfa21, cs21fa_res)
fetch_and_save(link_cssp22, cs22sp_res)

# %%
with open(cs22sp_res, 'r') as f:
    cs22sp = json.load(f)

with open(cs21fa_res, 'r') as f:
    cs21fa = json.load(f)

with open(links, 'r') as f:
    prereq_link = json.load(f)

name_list = []
cs22 = []
for course in cs22sp:
    cs22.append(course)
    name_list.append(course["name"])
for course in cs21fa:
    if course["name"] not in name_list:
        cs22.append(course)

prereqs = []
for course in cs22:
    # promote recitations to attribute of course instead of section
    recitations = []
    for section in course["sections"]:
        if "recitations" in section:
            for recitation in section["recitations"]:
                recitations.append(recitation)
            section.pop("recitations")
    course['recitations'] = recitations
    
   
    # if "prerequisites" in course["sections"][0]:
        # prereqs.append(course["sections"][0]["prerequisites"])
        # print(course["subjectCode"]["code"] + '-' + course["subjectCode"]["school"] + '-'+ course["deptCourseId"] + '-'+  course["name"] + ' ' +re.sub('\n', ' ', course["sections"][0]["prerequisites"]))
    # else:
    #     print(course["name"])
    # print(course["name"])
    
    course_index = course["subjectCode"]["code"] + '-' + course["subjectCode"]["school"] + '-'+ course["deptCourseId"] + '-'+  course["name"]
    if course_index in prereq_link:
        course["prerequisites"] = prereq_link[course_index]
    else:
        course["prerequisites"] = []

    
with open(cs_cleaned, 'w') as f:
    json.dump(cs22, f, indent=True)

# %%
with open(cs_cleaned, 'r') as f:
    data = json.load(f)

result = {}
for course in data:
    
    # organize courses by course level
    course_level = course["deptCourseId"]
    course_level = course_level[0] + (len(course_level) - 1) * '0'
    # print(course_level)
    if course_level in result:
        result[course_level].append(course)
    else:
        result[course_level] = [course]
for value in result.values():
    value.sort(key = lambda x: int(x["deptCourseId"]))
    print([i["deptCourseId"] for i in value])

with open(cs_orgranized, 'w') as f:
    json.dump(result, f, indent=True)


