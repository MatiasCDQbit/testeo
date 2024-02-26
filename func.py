import io
import json
import logging
import requests

from fdk import response


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info('==========INICIOBUSCARCOMPANIAS==========')
    token = "##########tokenTEST##########"
    try:
        cfg = ctx.Config()
        urlOrc = cfg["urlLogin"]
        params = {
            "P0010_Version": "", 
            "token": token
        }

    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))


    respuesta = sendQuery(params,urlOrc)
    respJson  = procesarRespuesta(respuesta)


    return response.Response(
        ctx, response_data=json.dumps(
            {"message": respJson}),
        headers={"Content-Type": "application/json"}
    )



def sendQuery(params,urlOrc):
    url = urlOrc +'/PORTAL_buscar_companias'
    logging.getLogger().info({'url': url})
    try:
        auth_data = params
        
        resp = requests.post(url, json=auth_data)
        logging.getLogger().info(resp)
    except Exception as e:
        resp = "Falló: " + str(e)
    return resp



def procesarRespuesta(respuesta):
    logging.getLogger().info(respuesta)
    
    resultado= {respuesta}
    if (respuesta.status_code is not None and respuesta.status_code < 400):
        respJson = respuesta.json()
        if respJson['jde__status'] is "SUCCESS":
             resultado = {
	            "success"         : True,
	            "rowset"          : respJson['rowset'],
	            "data"            : None,
	            "errorJde"        : None,
	            "errorsList"      : None
             }
        else:
            resultado =  {
	            "success"         : True,
	            "rowset"          : None,
	            "data"            : None,
	            "errorJde"        : False,
	            "errorsList"      : respuesta
             }
    else:  
        logging.getLogger().info(respuesta)
        
        resultado =  {
	            "success"         : False,
	            "rowset"          : None,
	            "data"            : None,
	            "errorJde"        : False,
	            "errorsList"      : respuesta
             }
    logging.getLogger().info(resultado)
    return resultado