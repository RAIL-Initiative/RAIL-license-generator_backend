# generate all combinations of licenses with Jinja

import itertools
import os

from jinja2 import Environment, FileSystemLoader, Template


def generate_license_combinations():
    
    # use all combinations of license, artefacts and derivatives/researchOnly
    licenses = ['OpenRAIL', 'ResearchRAIL', 'RAIL']
    artifacts = ['', 'A', 'M', 'S', 'AS', 'AM', 'MS', 'AMS']
    combinations = itertools.product(licenses, artifacts)

    # generate a list of all combinations
    license_combinations = []
    for combination in combinations:
        combination = {
            'license': combination[0],
            'artifact': combination[1],
            'reuse_distribution': combination[0] != "RAIL",
        }
        LICENSE_NAME= f"{combination['license']}-{combination['artifact']}"

        if combination['reuse_distribution'] or combination['license'] == "ResearchRAIL":
            TARGET_OBJECT="Artifact(s) and Modifications of the Artifact(s)"
        else:
            TARGET_OBJECT="Artifact(s)"

        ARTIFACT = []
        if "A" in combination['artifact']:
            ARTIFACT.append("Application")
        if "M" in combination['artifact']:
            ARTIFACT.append("Model")
        if "S" in combination['artifact']:
            ARTIFACT.append("Source Code")
        ARTIFACT = ", ".join(ARTIFACT)
        if len(ARTIFACT) == 0:
            ARTIFACT = ""
                
        license_combinations.append({
        "LICENSE_NAME": LICENSE_NAME,
        "TARGET_OBJECT": TARGET_OBJECT,
        "ARTIFACT": ARTIFACT,
        "LICENSE_TYPE": combination['license'],
        "RESTRICTIONS": [],
        "REUSE_DISTRIBUTION": combination['reuse_distribution'],
        })
        
    return license_combinations


def generate_license_text(license_combinations):
    
    # load jinja template
    #print current path
    print(os.getcwd())
    with open('backend/app/app/templates/license.jinja') as file_:
        template = Template(file_.read())
    
    # generate license text for each combination
    licenses = []
    for combination in license_combinations:
        
        licenses.append({
            'LICENSE_TYPE': combination['LICENSE_TYPE'],
            'ARTIFACT': combination['ARTIFACT'],
            'REUSE_DISTRIBUTION': combination['REUSE_DISTRIBUTION'],
            'text': template.render(**combination)
        })
        
    return licenses

def main():
    
    # generate all combinations of licenses
    license_combinations = generate_license_combinations()
    
    # generate license text for each combination
    licenses = generate_license_text(license_combinations)

    # create folder if it does not exist
    folder = f"./all_licenses"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # write all licenses to seperate files in folders with their parameters in the file name
    for license in licenses:
        # write license text to file

        filename = f"{folder}/license={license['LICENSE_TYPE']}-artefact={license['ARTIFACT']}.txt"
        with open(filename, "w") as f:
            f.write(license['text'])
            f.close()

main()