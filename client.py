import python3_gearman as gearman

def check_request_status(job_request):
   # if job_request.complete:
   print ("Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result))
   # elif job_request.timed_out:
   #     print "Job %s timed out!" % job_request.unique

gm_client = gearman.GearmanClient(['localhost:4730'])

arquivo_imagem = "/home/diego/projetos/ferias2018.2/core/mnist/fotos_teste/0.png"
completed_job_request = gm_client.submit_job("process", '{"data":"%s"}' % arquivo_imagem)
check_request_status(completed_job_request)

print ("Exception:",completed_job_request.exception)
print ("Warnings:",', '.join(completed_job_request.warning_updates))
print ("Result:",completed_job_request.result)
print ('Work complete with state %s' % completed_job_request.state)

