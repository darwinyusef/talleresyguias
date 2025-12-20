package main

import (
    "github.com/gofiber/fiber/v2"
    "log"
)

func main() {
    app := fiber.New()

    app.Get("/", func(c *fiber.Ctx) error {
        return c.JSON(fiber.Map{
            "message": "Go Fiber is blazing fast with GitHub Actions!",
        })
    })

    app.Get("/health", func(c *fiber.Ctx) error {
        return c.SendStatus(200)
    })

    log.Fatal(app.Listen(":3000"))
}
