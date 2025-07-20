#!/usr/bin/env python3

import argparse

from kubernetes import client, config
from tabulate import tabulate
from colorama import Fore, Style

# Kubernetes client config
config.load_kube_config()     
v1 = client.CoreV1Api()

# Argument parser config
parser = argparse.ArgumentParser(
    description='List pods in all namespaces',
    prog='get-all-pods.py'
)
parser.add_argument("-n", "--namespace", help="Filter specific namespace" )

TABLE_HEADERS = [
    f'{Style.BRIGHT}Namespace{Style.RESET_ALL}',
    f'{Style.BRIGHT}Pod{Style.RESET_ALL}',
    f'{Style.BRIGHT}Images{Style.RESET_ALL}'
]

def get_pods_all_namespaces() -> list:
    return v1.list_pod_for_all_namespaces(watch=False).items

def get_pods_specific_namespace(namespace) -> list:
    return v1.list_namespaced_pod(namespace=namespace).items

def get_pod_images(pod) -> list:
    return [ container.image for container in pod.spec.containers ]

def add_to_table(pod, table):
    images = get_pod_images(pod)
    fmt_images = ', '.join(images)
    table.append([color_cyan(pod.metadata.namespace), color_magenta(pod.metadata.name), color_blue_light(fmt_images)])

def color_cyan(text: str) -> str:
    return f'{Fore.CYAN}{text}{Style.RESET_ALL}'

def color_magenta(text: str) -> str:
    return f'{Fore.MAGENTA}{text}{Style.RESET_ALL}'

def color_blue_light(text: str) -> str:
    return f'{Fore.LIGHTBLUE_EX}{text}{Style.RESET_ALL}'

def output_all_pods(namespace=None) -> None:
    
    pods = get_pods_all_namespaces() if namespace == None else get_pods_specific_namespace(namespace)
    if len(pods) == 0:
        print('No pods found.')
        return
    
    table = []
    for pod in pods:
        add_to_table(pod, table)
    output = tabulate(table, headers=TABLE_HEADERS)
    print(output)

def main():
    args = parser.parse_args()
    output_all_pods(args.namespace)

if __name__ == '__main__':
    main()