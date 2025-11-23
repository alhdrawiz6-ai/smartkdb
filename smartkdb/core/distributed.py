import requests
import json
from typing import List, Dict, Any

class NodeManager:
    def __init__(self, my_address: str, peers: List[str] = None):
        self.my_address = my_address
        self.peers = peers or []
        self.status = "standalone"

    def join_cluster(self, seed_node: str):
        """
        Join an existing cluster via a seed node.
        """
        try:
            response = requests.post(f"{seed_node}/cluster/join", json={"address": self.my_address})
            if response.status_code == 200:
                data = response.json()
                self.peers = data.get("peers", [])
                self.status = "clustered"
                print(f"Successfully joined cluster via {seed_node}")
            else:
                print(f"Failed to join cluster: {response.text}")
        except Exception as e:
            print(f"Error joining cluster: {e}")

    def broadcast_update(self, table: str, record_id: str, data: Dict[str, Any]):
        """
        Broadcast a data update to all peers.
        """
        if self.status != "clustered":
            return

        for peer in self.peers:
            if peer == self.my_address:
                continue
            
            try:
                # Fire and forget for now, or use a queue
                requests.post(f"{peer}/sync/update", json={
                    "table": table,
                    "id": record_id,
                    "data": data
                }, timeout=1)
            except:
                pass # Peer might be down

    def get_cluster_status(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "my_address": self.my_address,
            "peers": self.peers
        }
