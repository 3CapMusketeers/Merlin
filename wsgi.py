from main import app

app.config['DEBUG'] = False

apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2020-10-16T16:16:18Z"
  finalizers:
  - service.kubernetes.io/load-balancer-cleanup
  labels:
    io.kompose.service: lancelot
  name: lancelot-service
  namespace: default
  resourceVersion: "3218236"
  selfLink: /api/v1/namespaces/default/services/lancelot-service
  uid: bf650d7c-dc23-4a5d-a1b4-a45813886b43
spec:
  clusterIP: 10.4.15.196
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 30417
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    io.kompose.service: lancelot
  sessionAffinity: None
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 35.185.100.45
