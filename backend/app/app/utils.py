import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from jose import jwt

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
    

def generate_license_text(license_type: Literal["OpenRAIL", "ResearchRAIL"], artifact_type: Literal["A", "M", "S", "AS", "AM", "AMS"] ="M") -> str:
    if license_type.strip() =="OpenRAIL":
        print("Generating OpenRAIL")
        reuse_distribution=True
        research_rail=False
    elif license_type.strip()== "ResearchRAIL":
        print("Generating ResearchRAIL")
        reuse_distribution=True
        research_rail=True
    else:
        print("Unsupported type -- generating RAIL")
        reuse_distribution=False
        research_rail=False


    license_name=license_type+"-"+artifact_type

    if reuse_distribution or research_rail:
        TARGET_OBJECT="Artifact(s) and Modifications of the Artifact(s)"
    else:
        TARGET_OBJECT="Artifact(s)"

    ARTIFACT = []
    if "A" in artifact_type:
        ARTIFACT.append("Application")
    if "M" in artifact_type:
        ARTIFACT.append("Model")
    if "S" in artifact_type:
        ARTIFACT.append("Source Code")
    ARTIFACT = ", ".join(ARTIFACT)
    if len(ARTIFACT) == 0:
        ARTIFACT = "============ERROR CHECK LICENSE=========="


    PERMITTED_PURPOSE=""

    if research_rail:
        PERMITTED_PURPOSE="q. “Permitted Purpose” means for academic or research purposes only."




    license_text="""Section I: Preamble

    This """+license_name+""" license strives for both the open and responsible Use of the accompanying Artifact(s). Openness here is understood as enabling users of the Artifact(s) on a royalty free basis to Use it, modify it, and even share commercial versions of it. Use restrictions are included to prevent misuse of the licensed Artifacts.

    This License Agreement governs the Use of the """+TARGET_OBJECT+""". You and Licensor agree as follows:

    1. Definitions

    a. “Contribution” means any work of authorship, including the original version of the Artifact and any Modifications of the Artifact that is intentionally submitted to Licensor for inclusion in the Artifact by the copyright owner or by an individual or entity authorized to submit on behalf of the copyright owner. For the purposes of this definition, “submitted” means any form of electronic, verbal, or written communication sent to the Licensor or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor for the purpose of discussing and improving the Artifact, but excluding communication that is conspicuously marked or otherwise designated in writing by the copyright owner as “Not a Contribution.”

    b. “Contributor” means Licensor and any individual or entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Artifact(s).

    c. “Data” means a collection of information extracted from the dataset used with the Model, including to train, pretrain, or otherwise evaluate the Model. The Data is not licensed under this License Agreement.

    d. “Explanatory Documentation” means model cards, data cards, or any other similar documentation or related information dedicated to inform the public about the characteristics of the model. Explanatory documentation is not licensed under this license.

    e. “Harm” includes but is not limited to physical, mental, psychological, financial and reputational damage, pain, or loss.

    f. “License Agreement” means this document.

    g. “Licensor” means the rights owners or entity authorized by the rights owners that are granting the terms and conditions of this License Agreement.

    h. “Model” means machine-learning based assemblies (including checkpoints), consisting of learnt weights and parameters (including optimizer states), corresponding to a model architecture as embodied in source code. Source code is not licensed under this License Agreement.

    i. "Source Code" means ......

    j. "Application" means ......

    i. "Artifact(s)" means the """+ARTIFACT+""" or a subset thereof

    j. “Modifications of the Artifact(s)” means all changes to the """+ARTIFACT+""" or any other model which is created or initialized by transfer of patterns of the weights, parameters, activations or Output of the Model.

    k. “Output” means the results of operating the Model.

    l. “Share” means any transmission, reproduction, publication or other sharing of the Artifact or Modifications of the Artifact to a third party, including providing the Artifact as a hosted service made available by electronic or other remote means, including - but not limited to - API-based or web access.

    m. “Third Parties” means individuals or legal entities that are not under common control with Licensor or You.

    n. “Use” includes - but is not limited to - generating any Output, fine tuning, updating, running, training, evaluating and/or reparametrizing the Model.

    p. “You” (or “Your”) means an individual or Legal Entity exercising permissions granted by this License Agreement and/or making Use of the Artifact(s) for whichever purpose and in any field of Use.

    """+PERMITTED_PURPOSE+"""


    Section II: INTELLECTUAL PROPERTY RIGHTS

    The """+TARGET_OBJECT+""" are subject to additional terms as described in Section III, which shall govern the Use of the """+TARGET_OBJECT+"""

        Grant of Copyright license. Subject to the terms and conditions of this License Agreement and where and as applicable, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, copyright license to reproduce, prepare, publicly display, publicly perform, sublicense under the terms herein, and distribute """+TARGET_OBJECT+""".

        Grant of Patent license. Subject to the terms and conditions of this License Agreement and where and as applicable, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free patent license to make, have made, Use, offer to sell, sell, import, and otherwise transfer the Artifact(s), where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Artifact(s) to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Artifact(s) or a Contribution incorporated within the Artifact(s) constitutes direct or contributory patent infringement, then any rights granted to You under this License Agreement for the Artifact(s) shall terminate as of the date such litigation is filed.

    Section III: CONDITIONS OF USE

    4. Use conditions. Compliance with the restrictions in Attachment A is a condition to the grants in this License Agreement. If You Use the Artifact(s), You agree not to Use it for the specified restricted uses set forth in Attachment A.

    5. Sharing of the Artifact(s)"""

    SHARING_YES="""

    5.1. You may Share the """+TARGET_OBJECT+""" under any license of your choice that does not contradict the restrictions in Attachment A of this License Agreement and includes:

    a. Paragraph 4 and the restrictions in Attachment A of this License Agreement, or,

    b. Use conditions similar to Paragraph 4 that must accomplish the same purpose as the use conditions in Paragraph 4 and a similar set of restrictions to those in Attachment A that must accomplish the same purpose as the restrictions in Attachment A.

    5.2. When You Share the """+ TARGET_OBJECT+""", You agree to:

    a. Give any recipients a copy of this License Agreement;

    b. Retain all Explanatory Documentation; <DELETE>and if sharing Modifications of the Artifact(s), add Explanatory Documentation of the same or better quality documenting the changes made to create the Modifications of the Artifact(s)</DELETE>; and

    c. Retain all copyright, patent, trademark, and attribution notices.
    
    """

    RESEARCH_USE_SHARING="""d. You and any Third Party recipients of the """+TARGET_OBJECT+"""  must adhere to the Permitted Purpose.

    """


    SHARING_NO="ALERT:You may not distribute the Artifact or its copies -- CHECK WITH JENNY ==========="

    if not reuse_distribution and not research_rail:
        license_text=license_text+" "+SHARING_NO
    else:
        license_text=license_text+" "+SHARING_YES
        if research_rail:
            license_text=license_text+RESEARCH_USE_SHARING

    license_text=license_text + """"
    6. The Output You Generate. Licensor claims no rights in the Output. You agree not to contravene any provision as stated in the License Agreement with your Use of the Output.
    Section IV: OTHER PROVISIONS

    7. Updates and Runtime Restrictions. Licensor reserves the right to restrict (remotely or otherwise) usage of the Artifact(s) in violation of this License Agreement.

    8. Submission of Contributions. Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Artifact(s) by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions. Notwithstanding the above, nothing herein shall supersede or modify the terms of any separate license agreement you may have executed with Licensor regarding such Contributions.

    9. Trademarks and related. Nothing in this License Agreement permits You to make Use of Licensors’ trademarks, trade names, logos or to otherwise suggest endorsement or misrepresent the relationship between the parties; and any rights not expressly granted herein are reserved by the Licensors.

    10. Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Artifact(s) (and each Contributor provides its Contributions) on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or sharing the Artifact(s)and Modifications of the Artifact(s), and assume any risks associated with Your exercise of permissions under this License Agreement.

    11. Limitation of Liability. In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License Agreement or out of the Use or inability to Use the Artifact(s) (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, model failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.

    12. Accepting Warranty or Additional Liability. While sharing the """+ TARGET_OBJECT+"""  thereof, You may choose to offer and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License Agreement. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.

    13. This License Agreement is a license of copyright and patent rights and an agreement in contract between You and the Licensor. If any provision of this License Agreement is held to be invalid, illegal or unenforceable, the remaining provisions shall be unaffected thereby and remain valid as if such provision had not been set forth herein.

    END OF TERMS AND CONDITIONS
    Attachment A - USE RESTRICTIONS

    You agree not to Use the"""+TARGET_OBJECT+" :"

    # (a) In any way that violates any applicable national, federal, state, local or international law or regulation;

    # (b) For the purpose of exploiting, Harming or attempting to exploit or harm minors in any way;

    # (c) To generate and/or disseminate malware (including - but not limited to - ransomware) or any other content to be used for the purpose of Harming electronic systems;

    # (d) To generate or disseminate verifiably false information and/or content with the purpose of Harming others;

    # (e) To generate or disseminate personal identifiable information with the purpose of Harming others;

    # (f) To generate or disseminate information (including - but not limited to - images, code, posts, articles), and place the information in any public context (including - but not limited to - bot generating tweets) without expressly and intelligibly disclaiming that the information and/or content is machine generated;

    # (g) To intentionally defame, disparage or otherwise harass others;

    # (h) To impersonate or attempt to impersonate human beings for purposes of deception;

    # (i) For fully automated decision making that adversely impacts an individual’s legal rights or otherwise creates or modifies a binding, enforceable obligation without expressly and intelligibly disclaiming that the creation or modification of the obligation is machine generated;

    # (j) For any Use intended to discriminate against or Harm individuals or groups based on online or offline social behavior or known or predicted personal or personality characteristics;

    # (k) To intentionally exploit any of the vulnerabilities of a specific group of persons based on their age, social, physical or mental characteristics, in order to materially distort the behavior of a person pertaining to that group in a manner that causes or is likely to cause that person or another person physical or psychological harm;

    # (l) For any Use intended to discriminate against individuals or groups based on legally protected characteristics or categories;

    # (m) To provide medical advice or medical results interpretation that is intended to be a substitute for professional medical advice, diagnosis, or treatment;

    # (n) For fully automated decision making in administration of justice, law enforcement, immigration or asylum processes."""

    return license_text
