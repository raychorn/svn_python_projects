Packaging Python as a Microsoft Installer Package (MSI)
=======================================================

Using this library, Python can be packaged as a MS-Windows
MSI file. To generate an installer package, you need
a build tree, whose location is currently hard-coded in
msi.py. You also need to edit msi.py to list the correct
Python version of the binaries you are going to package.

The packaging process assumes that binaries have been 
generated according to the instructions in PCBuild/README.txt,
and that you have either Visual Studio or the Platform SDK
installed. In addition, you need the Python COM extensions,
either from PythonWin, or from ActivePython.

To invoke the script, open a cmd.exe window which has 
cabarc.exe in its PATH (e.g. "Visual Studio .NET 2003
Command Prompt"). Then invoke

<path-to-python.exe> msi.py

If everything succeeds, pythonX.Y.Z.msi is generated
in the current directory.

Microsoft Sample Code
---------------------

This library is partially based on Microsoft sample code,
from the Samples/sysmgmt/msi/database directory of the
platform SDK. In particular, the files

exclamic.bin
info.bin
New.bin
Up.bin

are extracted from UISample.msi, and can be distributed
only according to the licensing restrictions shown below.

END-USER LICENSE AGREEMENT FOR MICROSOFT SOFTWARE

MICROSOFT PLATFORM SOFTWARE DEVELOPMENT KIT

IMPORTANT-READ CAREFULLY: This End-User License Agreement ("EULA") is a legal agreement between you (either an individual or a single entity) and Microsoft Corporation for the Microsoft software that accompanies this EULA, which includes computer software and may include associated media, printed materials, "online" or electronic documentation, and Internet-based services ("Software").  An amendment or addendum to this EULA may accompany the Software.  YOU AGREE TO BE BOUND BY THE TERMS OF THIS EULA BY INSTALLING, COPYING, OR OTHERWISE USING THE SOFTWARE. IF YOU DO NOT AGREE, DO NOT INSTALL, COPY, OR USE THE SOFTWARE; YOU MAY RETURN IT TO YOUR PLACE OF PURCHASE FOR A FULL REFUND, IF APPLICABLE.

 

1.         GRANT OF LICENSE.  Microsoft grants you the rights described in this EULA provided that you comply with all terms and conditions of this EULA. 

1.1       General License Grant.  Microsoft grants you a limited, nonexclusive license to use the Software, and to make and use copies of the Software, for the purposes of designing, developing and testing your software applications for use with any version or edition of a Microsoft Windows operating system for personal computers or servers ("Microsoft Operating System Product"). 

1.2       Sharepoint Portal Server SDK.  The Software contains the SharePoint Portal Server Software Development Kit ("SPSSDK").  In addition to the license granted in Section 1.1, Microsoft grants you a limited, nonexclusive license to modify the sample source code located in the SPSSDK solely to design, develop, and test your application internally within your organization.  Your entire license under this EULA with respect to the SPSSDK is conditioned on your not using the SPSSDK to create software that is incompatible with file formats indexed by Microsoft SharePoint Portal Server 2001. 

2.         Additional License Rights -- Redistributable COMPONENTS

2.1       Source Code.  "Source Code" means source code that is located in any directory or sub-directory named "samples" in the Software or that is otherwise identified as sample code in the Software, other than source code included in the SPSSDK, or is identified as Microsoft Foundation Class Libraries ("MFC"), Template Libraries ("ATL"), and C runtimes (CRTs).  Microsoft grants you a limited, nonexclusive license (a) to use and modify any Source Code to design, develop, and test your software applications;  and (b) to make and distribute copies of the Source Code and your modifications, subject to your compliance with Section 3. 

2.2       Redistributable Code.  All portions of the Software that are listed in the text file \License\Redist.txt collectively constitute "Redistributable Code."  Microsoft grants you a limited, nonexclusive license to reproduce and distribute Redistributable Code in object code form only, subject to your compliance with Section 3. 

3.         DISTRIBUTION REQUIREMENTS AND LICENSE LIMITATIONS

3.1       Your licenses under Section 2 to distribute Source Code, any modifications you make to the Source Code under Section 2.1, and Redistributable Code (collectively, "Redistributables") are conditioned on the following:  (a) you will distribute Redistributables only in object code form and in conjunction with and as a part of a software application developed by you that adds significant and primary functionality to the Redistributables ("Application"); (b) the Redistributables will operate only in conjunction with a Microsoft Operating System Product; (c) your Application will invoke the Software only via interfaces described in the documentation accompanying the Software; (d) you will distribute your Application containing the Redistributables only pursuant to an end-user license agreement (which may be break-the-seal, click-wrap or signed) with terms no less protective than those contained in this EULA; (e) you will not use Microsoft’s name, logo, or trademarks to market your Application; (f) you will include a valid copyright notice on your Application sufficient to protect Microsoft’s copyright in the Software; (g) you will not remove or obscure any copyright, trademark or patent notices that appear on or in the Software as delivered to you; (h) you will indemnify, hold harmless, and defend Microsoft from and against any claims or lawsuits, including attorneys’ and experts’ fees, that arise or result from the use or distribution of your Application; and (i) you will otherwise comply with the terms of this EULA.  You may not permit further distribution of Redistributables by your end users except that you may permit further redistribution of Redistributables by your distributors to end users if your distributors only distribute the Redistributables in conjunction with and as part of your Application or Applications, you comply with all other terms of this EULA, and your distributors comply with all restrictions of this EULA that are applicable to you. 

3.2       Renaming MFC, ATL or CRTs.  You must rename all files containing MFC, ATL or CRTs prior to distributing them or any modifications to them. 

3.3       Linking .lib Files.  For any Redistributable Code having a filename extension of .lib, you may distribute only the results of running such Redistributable Code through a linker with your application. 

3.4       Notice for Windows Media Technologies.  In each Application in which you include any Redistributables from the Windows Media Player SDK, Windows Media Services SDK, Windows Media Encoder SDK, or Windows Media Software Development Kit (including but not limited to, the Windows Media Format SDK) portions of the Software, you must include in your Application’s Help-About box (or if there is no such box, then in another location that end users will easily discover), a copyright notice stating the following:  "Portions utilize Microsoft Windows Media Technologies.  Copyright (c) 1999-2002 Microsoft Corporation.  All Rights Reserved." 

3.5       No Alteration to Setup Programs.  If any Redistributables in the Software as delivered to you are contained in a separate setup program, then you may only distribute those Redistributables as part of that setup program, without alteration to that setup program or removal of any of its components. 

3.6       Prerelease Code.  The Software may contain prerelease code that might not operate correctly, is not at the level of performance and compatibility of the final, generally available product offering, and might be substantially modified prior to shipment of that offering.  Microsoft is not obligated to make this or any later version of the Software commercially available.  Your license under Section 2 to distribute any Redistributables identified in the documentation as prerelease, alpha, beta or release candidate code or under a similar designation indicating code that is not intended for commercial distribution (collectively, "Prerelease Code") is conditioned upon your marking the version of your Application containing the Prerelease Code as "BETA," "PRE-RELEASE" or other reasonable designation of similar import.  Your license under this Section 3.3 terminates upon Microsoft’s publicly announced commencement of the commercial availability of the Microsoft Operating System Product for which your Application is developed. 

3.7       Identified Software.  If you use the Redistributables, then in addition to your compliance with the applicable distribution requirements described for the Redistributables, the following also applies.  Your license rights to Redistributables are conditioned on your (a) not incorporating Identified Software into or combining Identified Software with the Redistributables;  (b) not distributing Identified Software in conjunction with the Redistributables;  and (c) not using Identified Software in the development of a derivative work of Source Code.  "Identified Software" means software that is licensed pursuant to terms that directly or indirectly create, or purport to create, obligations for Microsoft with respect to the Redistributables or grant, or purport to grant, to any third party any rights or immunities under Microsoft’s intellectual property or proprietary rights in the Redistributables.  Identified Software includes, without limitation, any software that requires as a condition of its use, modification and/or distribution that any other software incorporated into, derived from or distributed with such software must also be disclosed or distributed in source code form, licensed for the purpose of making derivative works, or redistributable at no charge. 

4.         COMPONENT EULAS.  As a kit of development tools and other Microsoft software programs (each such tool or software program, a "Component"), the Software may contain one or more Components for which a separate end-user license agreement (a "Component EULA") may appear upon installation of the applicable Component.  In the event of inconsistencies between this EULA and any Component EULA, the terms of the Component EULA will control as to the applicable Component. 

5.         RESERVATION OF RIGHTS AND OWNERSHIP. The Software is licensed, not sold.  Microsoft reserves all rights not expressly granted to you in this EULA.  The Software is protected by copyright and other intellectual property laws and treaties. Microsoft or its suppliers own the title, copyright, and other intellectual property rights in the Software. 

6.         LIMITATIONS ON REVERSE ENGINEERING, DECOMPILATION, AND DISASSEMBLY.  You may not reverse engineer, decompile, or disassemble the Software, except and only to the extent that such activity is expressly permitted by applicable law notwithstanding this limitation.

7.NO RENTAL OR COMMERCIAL HOSTING.  You may not rent, lease, lend or provide commercial hosting services with the Software.

8.         CONSENT TO USE OF DATA.You agree that Microsoft and its affiliates may collect and use technical information gathered as part of the product support services provided to you, if any, related to the Software.  Microsoft may use this information solely to improve our products or to provide customized services or technologies to you and will not disclose this information in a form that personally identifies you. 

9.         LINKS TO THIRD-PARTY SITES.  You may link to third-party sites through the use of the Software.  The third-party sites are not under the control of Microsoft, and Microsoft is not responsible for the contents of any third-party sites, any links contained in third-party sites, or any changes or updates to third-party sites.  Microsoft is not responsible for web-casting or any other form of transmission received from any third-party sites.  Microsoft is providing these links to third-party sites to you only as a convenience, and the inclusion of any link does not imply an endorsement by Microsoft of the third-party site.

10.       ADDITIONAL SOFTWARE OR SERVICES.  This EULA applies to updates, supplements, add-on components or Internet-based services components of the Software that Microsoft may provide to you or make available to you after the date you obtain your initial copy of the Software, unless Microsoft provides other terms along with the update, supplement, add-on component, or Internet-based services component.  Microsoft reserves the right to discontinue any Internet-based services provided to you or made available to you through the use of the Software. 

11.       EXPORT RESTRICTIONS.  You acknowledge that the Software is subject to U.S. export jurisdiction.  You agree to comply with all applicable international and national laws that apply to the Software, including the U.S. Export Administration Regulations, as well as end-user, end-use, and destination restrictions issued by U.S. and other governments.  For additional information see <http://www.microsoft.com/exporting/>.

12.       SOFTWARE TRANSFER.  The initial user of the Software may make a one-time permanent transfer of this EULA and Software to another end user, provided the initial user retains no copies of the Software.  This transfer must include all of the Software (including all component parts, the media and printed materials, any upgrades, this EULA, and, if applicable, the Certificate of Authenticity).  The transfer may not be an indirect transfer, such as a consignment.  Prior to the transfer, the end user receiving the Software must agree to all the EULA terms.

13.       TERMINATION.  Without prejudice to any other rights, Microsoft may terminate this EULA if you fail to comply with the terms and conditions of this EULA.  In such event, you must destroy all copies of the Software and all of its component parts.

14.       DISCLAIMER OF WARRANTIES.  to the maximum extent permitted by applicable law, Microsoft and its suppliers provide the Software and support services (if any) AS IS AND WITH ALL FAULTS, and hereby disclaim all other warranties and conditions, whether express, implied or statutory, including, but not limited to, any (if any) implied warranties, duties or conditions of merchantability, of fitness for a particular purpose, of reliability or availability, of accuracy or completeness of responses, of results, of workmanlike effort, of lack of viruses, and of lack of negligence, all with regard to the Software and the provision of or failure to provide support or other services, information, software, and related content through the Software or otherwise arising out of the use of the Software.  ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION, OR NON-INFRINGEMENT WITH REGARD TO THE SOFTWARE.

15.       EXCLUSION OF INCIDENTAL, CONSEQUENTIAL AND CERTAIN OTHER DAMAGES.  To the maximum extent permitted by applicable law, in no event shall Microsoft or its suppliers be liable for any special, incidental, punitive, indirect, or consequential damages whatsoever (including, but not limited to, damages for loss of profits or confidential or other information, for business interruption, for personal injury, for loss of privacy, for failure to meet any duty including of good faith or of reasonable care, for negligence, and for any other pecuniary or other loss whatsoever) arising out of or in any way related to the use of or inability to use the SOFTWARE, the provision of or failure to provide Support OR OTHER Services, informaton, software, and related CONTENT through the software or otherwise arising out of the use of the software, or otherwise under or in connection with any provision of this EULA, even in the event of the fault, tort (including negligence), misrepresentation, strict liability, breach of contract or breach of warranty of Microsoft or any supplier, and even if Microsoft or any supplier has been advised of the possibility of such damages.

16.       LIMITATION OF LIABILITY AND REMEDIES.  Notwithstanding any damages that you might incur for any reason whatsoever (including, without limitation, all damages referenced herein and all direct or general damages in contract or anything else), the entire liability of Microsoft and any of its suppliers under any provision of this EULA and your exclusive remedy hereunder shall be limited to the greater of the actual damages you incur in reasonable reliance on the Software up to the amount actually paid by you for the Software or US$5.00. The foregoing limitations, exclusions and disclaimers (including sections 14, 15 AND 16) shall apply to the maximum extent permitted by applicable law, even if any remedy fails its essential purpose.

17.       U.S. GOVERNMENT LICENSE RIGHTS.  All Software provided to the U.S. Government pursuant to solicitations issued on or after December 1, 1995, is provided with the commercial license rights and restrictions described elsewhere herein.  All Software provided to the U.S. Government pursuant to solicitations issued prior to December 1, 1995, is provided with "Restricted Rights" as provided for in FAR, 48 CFR 52.227-14 (JUNE 1987) or DFAR, 48 CFR 252.227-7013 (OCT 1988), as applicable.

18.       APPLICABLE LAW.  If you acquired this Software in the United States, this EULA is governed by the laws of the State of Washington.  If you acquired this Software in Canada, unless expressly prohibited by local law, this EULA is governed by the laws in force in the Province of Ontario, Canada; and, in respect of any dispute which may arise hereunder, you consent to the jurisdiction of the federal and provincial courts sitting in Toronto, Ontario.  If you acquired this Software in the European Union, Iceland, Norway, or Switzerland, then local law applies.  If you acquired this Software in any other country, then local law may apply.

19.       ENTIRE AGREEMENT; SEVERABILITY.  This EULA (including any addendum or amendment to this EULA which is included with the Software) is the entire agreement between you and Microsoft relating to the Software and the support services (if any) and it supersedes all prior or contemporaneous oral or written communications, proposals and representations with respect to the Software or any other subject matter covered by this EULA.  To the extent the terms of any Microsoft policies or programs for support services conflict with the terms of this EULA, the terms of this EULA shall control.  If any provision of this EULA is held to be void, invalid, unenforceable or illegal, the other provisions shall continue in full force and effect.

Si vous avez acquis votre produit Microsoft au CANADA, la garantie limitée suivante vous concerne :

DÉNI DE GARANTIES.  Le Logiciel et les services de soutien technique (le cas échéant) sont fournis TELS QUELS ET AVEC TOUS LES DÉFAUTS par Microsoft et ses fournisseurs, lesquels par les présentes dénient toutes autres garanties et conditions expresses, implicites ou en vertu de la loi, notamment (le cas échéant) les garanties, devoirs ou conditions implicites de qualité marchande, d’adaptation à un usage particulier, d’exactitude ou d’exhaustivité des réponses, des résultats, des efforts déployés selon les règles de l’art, d’absence de virus et de négligence, le tout à l’égard du Logiciel et de la prestation des services de soutien technique ou de l’omission d’une telle prestation.  PAR AILLEURS, IL N’Y A AUCUNE GARANTIE OU CONDITION QUANT AU TITRE DE PROPRIÉTÉ, À LA JOUISSANCE OU LA POSSESSION PAISIBLE, À LA CONCORDANCE À UNE DESCRIPTION NI QUANT À UNE ABSENCE DE CONTREFAÇON CONCERNANT LE LOGICIEL.

EXCLUSION DES DOMMAGES ACCESSOIRES, INDIRECTS ET DE CERTAINS AUTRES DOMMAGES. DANS LA MESURE MAXIMALE PERMISE PAR LES LOIS APPLICABLES, EN AUCUN CAS MICROSOFT OU SES FOURNISSEURS NE SERONT RESPONSABLES DES DOMMAGES SPÉCIAUX, CONSÉCUTIFS, ACCESSOIRES OU INDIRECTS DE QUELQUE NATURE QUE CE SOIT (NOTAMMENT, LES DOMMAGES À L’ÉGARD DU MANQUE À GAGNER OU DE LA DIVULGATION DE RENSEIGNEMENTS CONFIDENTIELS OU AUTRES, DE LA PERTE D’EXPLOITATION, DE BLESSURES CORPORELLES, DE LA VIOLATION DE LA VIE PRIVÉE, DE L’OMISSION DE REMPLIR TOUT DEVOIR, Y COMPRIS D’AGIR DE BONNE FOI OU D’EXERCER UN SOIN RAISONNABLE, DE LA NÉGLIGENCE ET DE TOUTE AUTRE PERTE PÉCUNIAIRE OU AUTRE PERTE DE QUELQUE NATURE QUE CE SOIT) SE RAPPORTANT DE QUELQUE MANIÈRE QUE CE SOIT À L’UTILISATION DU LOGICIEL OU À L’INCAPACITÉ DE S’EN SERVIR, À LA PRESTATION OU À L’OMISSION D’UNE TELLE PRESTATION DE SERVICES DE SOUTIEN TECHNIQUE OU AUTREMENT AUX TERMES DE TOUTE DISPOSITION DU PRÉSENT EULA OU RELATIVEMENT À UNE TELLE DISPOSITION, MÊME EN CAS DE FAUTE, DE DÉLIT CIVIL (Y COMPRIS LA NÉGLIGENCE), DE RESPONSABILITÉ STRICTE, DE VIOLATION DE CONTRAT OU DE VIOLATION DE GARANTIE DE MICROSOFT OU DE TOUT FOURNISSEUR ET MÊME SI MICROSOFT OU TOUT FOURNISSEUR A ÉTÉ AVISÉ DE LA POSSIBILITÉ DE TELS DOMMAGES.

LIMITATION DE RESPONSABILITÉ ET RECOURS.  Malgré les dommages que vous puissiez subir pour quelque motif que ce soit (notamment, tous les dommages susmentionnés et tous les dommages directs ou généraux), l’obligation intégrale de Microsoft et de l’un ou l’autre de ses fournisseurs aux termes de toute disposition du présent EULA et votre recours exclusif à l’égard de tout ce qui précède se limite au plus élevé entre les montants suivants : le montant que vous avez réellement payé pour le Logiciel ou 5,00 $US. Les limites, exclusions et dénis qui précèdent (y compris les clauses ci-dessus), s’appliquent dans la mesure maximale permise par les lois applicables, même si tout recours n’atteint pas son but essentiel.

La présente Convention est régie par les lois de la province d’Ontario, Canada. Chacune des parties à la présente reconnaît irrévocablement la compétence des tribunaux de la province d’Ontario et consent à instituer tout litige qui pourrait découler de la présente auprès des tribunaux situés dans le district judiciaire de York, province d’Ontario.

Au cas où vous auriez des questions concernant cette licence ou que vous désiriez vous mettre en rapport avec Microsoft pour quelque raison que ce soit, veuillez contacter la succursale Microsoft desservant votre pays, dont l’adresse est fournie dans ce produit, ou écrivez à : Microsoft Sales Information Center, One Microsoft Way, Redmond, Washington 98052-6399.

