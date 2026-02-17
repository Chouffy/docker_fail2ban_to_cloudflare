# Docker Fail2Ban to Cloudflare Firewall
This is an example of how to update Cloudflare Firewall with Fail2Ban data.

## Setup
- Install [Docker Fail2Ban](https://github.com/crazy-max/docker-fail2ban) with access to the log you want to monitor
- Copy the folder `fail2ban` in the Docker data container
- Setup the variables in `action.d/cf-waf-modifyBanList.py`, see top of the file
  - See [this blog post](https://kovasky.me/blogs/cloudflare_fail2ban/) for the required Cloudflare token
- (re)start the container
- Try a ban action
 - Double-check that origin IP is correct!
 - Unban with `fail2ban-client set <JAILNAME> unbanip XX.XX.XX.XX` from within the Docker container
- If successful, implement the List as a *Custom Rule* in Domain → Security → Security Rules

## Reference
- https://kovasky.me/blogs/cloudflare_fail2ban/ (where most code come from)
- https://blog.lrvt.de/securing-vaultwarden-with-fail2ban/
- https://github.com/crazy-max/docker-fail2ban
- https://github.com/dani-garcia/vaultwarden/wiki/Fail2Ban-Setup#testing-fail2ban
