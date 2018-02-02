# Here is the default bucket in Storage created with the project
# Update it respecting the format.
# Create sub directories described in the rest of this file.
DEFAULT_BUCKET_NAME = "/gnp-auttarifasgmm-qa.appspot.com/"

# Final Export Service
#
# Here is the bucket that contains uploaded every PBA files, and result of exportation
BUCKET_VF_NAME = DEFAULT_BUCKET_NAME + "Versiones_Finales/"
# Here is defined the folder here are stocked the INFO scripts files.
# WARNING: The folder is not created if not found. So don't delete it.
# If it has been deleted, just create a new /tmp folder.
BUCKET_VF_INFO_NAME = BUCKET_VF_NAME + "tmp/"
# Here is the file name that will have the PBA file once exported.
# It will be formatted like EXCEL_VF_FILE-<NextYear>
EXCEL_VF_FILE = "Productivas-adicionales-basicas.xlsx" 
# Here is the file name to search in /Versiones_Finales/ to create the Excel file
# during the exportation process.
# WARNING: The file is not created if not found. So don't delete it.
# If it has been deleted, just upload a new file named TEMPLATE_VF_FILE in BUCKET_VF_NAME folder.
TEMPLATE_VF_FILE = "Template_VF.xlsx"
# Here is the file name to create when all INFO scripts from /tmp/ are zipped.
# It is created at each process.
ZIP_VF_FILE = "Scripts_INFO.zip"

# Notifier
#
# Here is set the bucket containing the Contact files
# WARNING: The folder is not created if not found. So don't delete it.
# If it has been deleted, just create a new /Contactos folder.
BUCKET_CONTACT_NAME = DEFAULT_BUCKET_NAME + "Contactos/"
# Here is set the name of the Contact files
# WARNING: If the system doesn't find the file, the user will have no mean to know it.
# The file must have a new line for each contact to notify
# Lines must be formatted like: Mail <Space> Any comment
# WARNING: The <Space> is mandatory 
CONTACT_FILE = "Contactos.txt"
# Key to insert in the header
API_KEY = "l7xxa7482b574f8445d7ae1824af60dc2096"
# URL to send the request
URL = "https://api-qa.oscp.gnp.com.mx/notifier/notification/mail"

# Historic
#
# Here is the folder in which the Historic file is stored
# WARNING: The folder is not created if not found. So don't delete it.
# If it has been deleted, just create a new /Historico folder.
BUCKET_HISTORIC_NAME = DEFAULT_BUCKET_NAME + "Historico/"
HISTORIC_FILE = "Historico.txt"


# Catalog Service
#
# Here is the bucket in which will be stored the uploada catalogs.
# WARNING: The folder is not created if not found. So don't delete it.
# If it has been deleted, just create a new /Catalog folder
BUCKET_CATALOG_NAME = DEFAULT_BUCKET_NAME + "Catalog/"
# Here is the file name that will have the catalogs once exported.
# It will be formatted like CATALOG_FILE_NAME-HH-MM
CATALOG_FILE_NAME = "Catalogo.xlsx"


# Signed URL
#
# Here are parameters used to generate links to insert in the notifying mail.
# Please manipulate very cautiously, and respect the initial format. 
EXCEL_SIGNED_FILE = "Versiones_Finales/"
BUCKET_VF_SIGNED_NAME = "gnp-auttarifasgmm-qa.appspot.com"
SCRIPT_INFO = "Versiones_Finales/tmp/"

# Database
#
# Here is the name of the database
# you may check the connection parameters in 
# srcpy/Manager/SQLManager method __init__
DATABASE_NAME = "PBA"

