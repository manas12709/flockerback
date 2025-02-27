from api.jwt_authorize import token_required
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import subprocess
import re
import os

# Blueprint for Poll API
health_api = Blueprint('health_api', __name__, url_prefix='/api')
api = Api(health_api)

class HealthAPI(Resource):
    def get(self):
        try:
            # Run system commands with elevated privileges where needed
            raw_ram = subprocess.check_output(["sudo", "free", "-h"], stderr=subprocess.DEVNULL).decode("utf-8")
            raw_cpu = subprocess.check_output(["sudo", "top", "-bn1"], stderr=subprocess.DEVNULL).decode("utf-8")
            raw_disk = subprocess.check_output(["sudo", "df", "-h"], stderr=subprocess.DEVNULL).decode("utf-8")
            raw_network = subprocess.check_output(["sudo", "ip", "addr"], stderr=subprocess.DEVNULL).decode("utf-8")
        except subprocess.CalledProcessError:
            return jsonify({"error": "Permission denied or command failed"}), 500

        # Parse RAM (only total, used, free)
        ram_info = {}
        ram_line = re.search(r'Mem:\s+(\S+)\s+(\S+)\s+(\S+)', raw_ram)
        if ram_line:
            ram_info["total"] = ram_line.group(1)
            ram_info["used"] = ram_line.group(2)
            ram_info["free"] = ram_line.group(3)

        # Parse CPU (just idle, user, system)
        cpu_info = {}
        cpu_line = re.search(
            r'%Cpu\(s\):\s+([\d\.]+)\s+us,\s+([\d\.]+)\s+sy,\s+[\d\.]+\s+ni,\s+([\d\.]+)\s+id,.*',
            raw_cpu
        )
        if cpu_line:
            cpu_info["user"] = cpu_line.group(1)
            cpu_info["system"] = cpu_line.group(2)
            cpu_info["idle"] = cpu_line.group(3)

        # Parse Disk (example: only root device usage)
        disk_info = []
        for line in raw_disk.splitlines()[1:]:
            fields = line.split()
            if len(fields) >= 6 and fields[0].startswith("/dev/"):
                disk_info.append({
                    "filesystem": fields[0],
                    "size": fields[1],
                    "used": fields[2],
                    "avail": fields[3],
                    "use%": fields[4]
                })

        # Parse Network (just interface and inet lines)
        network_info = []
        for block in raw_network.split('\n\n'):
            if block.strip():
                iface_line = block.split('\n')[0].strip()
                inet_lines = [l.strip() for l in block.split('\n') if "inet " in l]
                network_info.append({
                    "interface": iface_line.split(':')[1].strip() if ':' in iface_line else iface_line,
                    "addresses": inet_lines
                })

        return jsonify({
            "ram": ram_info,
            "cpu": cpu_info,
            "disk": disk_info,
            "network": network_info
        })

api.add_resource(HealthAPI, "/health")
