from camo_sign import create_signed_url

base_url = 'https://camo.githubusercontent.com/'
secret_key = b'OMGWTFBBQ'
image_url = 'https://raw.githubusercontent.com/MrEnderman-YT/Network-City-Helper/refs/heads/main/Tag%20version.svg?token=GHSAT0AAAAAACYVRUIN6XAOMRKQK7BWDTLQZZSIA5Q'

ss = create_signed_url(base_url, secret_key, image_url)

print(ss)