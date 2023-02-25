#!/usr/bin/env python3

def split_certificates(string):
  list_of_certs = []
  list_of_lines = string.split("\n")
  for line in list_of_lines:
    if line == "-----BEGIN CERTIFICATE-----":
      temp_cert_list = []
      temp_cert_list.append(line)
    elif line == "":
      continue
    elif line == "-----END CERTIFICATE-----":
      temp_cert_list.append(line + "\n")
      certificate = "\n".join(temp_cert_list)
      list_of_certs.append(certificate)
    else:
      temp_cert_list.append(line)
  return list_of_certs


class FilterModule:
  def filters(self):
    return {"split_certificates": split_certificates}
