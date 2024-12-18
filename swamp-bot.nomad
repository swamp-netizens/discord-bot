job "swamp-discord-bot" {
  datacenters = ["dc1"]
  type = "service"

  group "bot" {
    count = 1

    task "discord-bot" {
      driver = "docker"

      config {
        image = "ghcr.io/swamp-netizens/discord-bot:main"
        force_pull = true

        # Mount the token file from the host into the container
        mount {
          type = "bind"
          source = "/etc/discord/token"
          target = "/app/token"
          readonly = true
        }
      }

      template {
        data = "{{ file \"/etc/discord/token\" }}"
        destination = "secrets/discord_token"
        change_mode = "restart"
      }

      env {
        DISCORD_TOKEN = "${NOMAD_SECRETS_DIR}/discord_token"
      }

      resources {
        cpu    = 200
        memory = 256
      }

      restart {
        attempts = 5
        interval = "5m"
        delay    = "25s"
        mode     = "delay"
      }
    }
  }
} 