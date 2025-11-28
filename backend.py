from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import shutil
import platform

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/directory', methods=['POST'])
def handle_directory():
    try:
        data = request.get_json()
        action = data.get('action')
        path = data.get('path', '')
        name = data.get('name', '')
        dest = data.get('dest', '')

        # Validate path exists for operations that need it
        if action in ['delete', 'move', 'organize'] and not os.path.exists(path):
            return jsonify({"success": False, "message": "Path does not exist"}), 404

        if action == 'create':
            full_path = os.path.join(path, name)
            os.makedirs(full_path, exist_ok=True)
            return jsonify({"success": True, "message": f"Created directory: {full_path}"})

        elif action == 'delete':
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return jsonify({"success": True, "message": f"Deleted: {path}"})

        elif action == 'move':
            shutil.move(path, dest)
            return jsonify({"success": True, "message": f"Moved to: {dest}"})

        elif action == 'organize':
            categories = {
                'Images': ['.png', '.jpg', '.jpeg', '.gif'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt'],
                'Archives': ['.zip', '.rar', '.7z']
            }

            for category, extensions in categories.items():
                os.makedirs(os.path.join(path, category), exist_ok=True)

            moved_files = 0
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    for category, extensions in categories.items():
                        if ext in extensions:
                            shutil.move(item_path, os.path.join(path, category, item))
                            moved_files += 1
                            break

            return jsonify({
                "success": True,
                "message": f"Organized {moved_files} files into categories"
            })

        return jsonify({"success": False, "message": "Invalid action"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)