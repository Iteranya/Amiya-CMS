# Amiya CMS

A lightweight content management system built with FastAPI, TinyDB, and vanilla web technologies. Amiya CMS includes direct integration with [Aina Website Creator](https://github.com/Iteranya/Aina-Website-Creator) for AI-assisted website generation and editing.

![Amiya](https://github.com/user-attachments/assets/164c4cf0-7bf4-4af2-a537-174bd1575b07)


## Features

- Simple admin interface for content management
- Page metadata and slug editing
- AI-powered website generation through Aina integration
- HTML content storage in TinyDB
- Built with minimal dependencies:
  - FastAPI
  - TinyDB
  - Vanilla JavaScript
  - CSS
  - HTML with Jinja templates
- Cloudflare integration for easy sharing

## ⚠️ Warning

**This project is still under development and lacks authentication/security features**. The admin panel is accessible through `/admin` without any login requirements. **DO NOT use in production environments!**

## Installation

### Windows
1. Clone the repository:
```
git clone https://github.com/Iteranya/Amiya-CMS.git
cd Amiya-CMS
```
2. Run the installation script:
```
start.cmd
```

### Linux/MacOS
1. Clone the repository:
```
git clone https://github.com/Iteranya/Amiya-CMS.git
cd Amiya-CMS
```
2. Create your own startup script based on the commands in `start.cmd`

## Usage

1. Access the admin panel at `/admin`
2. Edit website metadata and slugs
3. Use the integrated Aina Website Creator for AI-assisted content generation
4. Your pages will be stored in the TinyDB database

## Alternatives

If you're not experienced with homebrew CMS solutions, consider established alternatives like WordPress.

## Contributing

Feel free to submit issues and pull requests to help improve Amiya CMS.

## License

[MIT License](LICENSE)

## Project by

[Iteranya](https://github.com/Iteranya)

🐇 bnnuy
