import bjoern

from webapp import create_app

bjoern.listen(wsgi_app=create_app(), host="0.0.0.0", port=5000, reuse_port=True)
bjoern.run()
