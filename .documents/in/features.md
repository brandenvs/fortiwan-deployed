# Releases

**Engineer**: Branden v Staden.

## Fortiwan Dashboards V1

[[2024-02-19]]

> This standalone release of **"Fortiwan Dashboards"** effectively renders each network and its vitals as _GET_ data.
>
> Each network, if available, offers a WAN switch, which _PUT_ between the two providers present.
>
> These fully internet-driven WAN interfaces equip technicians with the necessary tools to monitor and respond to sites going down by switching the interface to the alternating provider
>
> ---

### Suite Feature List

1. **Alternating WAN Interface**. Endpoints are hit with a PUT action which contains instructions to change the interface's provider. Useful for when one provider is offline. [FAST-STABLE](V1)

2. **Direct-Support** where technicians lookup a specific serial number - **providing real-time support directly to the searched for site**. [STABLE](V1)

3. **All Sites** and **Unavailable Sites**  are featured buttons that will load sites, respectively. (Both are now functional from V1.2)

4. Bearer Token(APIUser objects) are dynamically handled based on a timed expiration of the token. **Refresher are used to refresh the Bearer Token**. [VULNERABLE](NO-CERTIFICATE)

5. **Thread executed** api requests are pooled together and bulked data is retrieved. The data is deconstructed into dynamic and interactive panes describing a site connected or disconnected from the network. [FAST-STABLE](V1)

6. **End-to-end** retrieval of _critical_ IPsec VPN Tunnel data in real-time. [STABLE](V1)

### Suite Compatibility Statement

All features that have been released within this suit is entirely dynamic, and adjusts certain properties to align with user screen size. The suit is built with a responsive design and leverages the well-known Bootstrap 5 Column and Grid technology to achieve this.

- Mobile Device Tested: **No(required)**
- Desktop & Laptop Device Tested: **Yes**
- Feedback: **10/10**

---
