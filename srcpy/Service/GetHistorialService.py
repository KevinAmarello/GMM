import logging
from flask import Response, json

from srcpy.Manager import StorageManager
import config


def handleService():
	logging.debug("GetHistorialService handleService Entry")
	listFilename = []
	listDate = []
	listResult = []

	bucketName = config.BUCKET_HISTORIC_NAME
	file = config.HISTORIC_FILE

	logging.debug("Opening History file")
	try:
		historyFile = StorageManager.openFile(bucketName + file, 'r')
		content = historyFile.read()
		historyFile.seek(0)
	except Exception as e:
		logging.debug(str(e))
		return Response("No archivo encontrado.", status = 500)

	try:
		logging.debug(content)
		for line in content.split("\n"):
			if line is not None and line != "":
				logging.debug(line)
				fline = line.split(" ")
				listFilename.append(fline[0])
				listDate.append(fline[1])
				try:
					listResult.append(fline[2])
				except:
					listResult.append("None")

		payload = {}
		payload["filename"] = listFilename
		payload["date"] = listDate
		payload["result"] = listResult

		logging.debug(str(payload))

		return Response(response = json.dumps(payload), status = 200, mimetype='application/json')
		#jsonify(payload), status = 200)
	except Exception as e:
		logging.debug(str(e))
		return Response("PLOP", status = 500)


