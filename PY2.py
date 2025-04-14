from Projectdir import app, db
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
from Projectdir.models import User,Post
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
