import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-xl border bg-card text-card-foreground shadow",
        className
      )}
      {...props}
    />
  )
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, CardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, uid, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
)

let PlayerCardDescription = React.forwardRef<HTMLParagraphElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <p
      ref={ref}
      className={cn("text-sm text-muted-foreground", className)}
      {...props}
    />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)

let PlayerCardFooter = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex items-center p-6 pt-0", className)}
      {...props}
    />
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCardDescription.displayName = "PlayerCardDescription"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardFooter.displayName = "PlayerCardFooter"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCardDescription = withClickable(PlayerCardDescription)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardFooter = withClickable(PlayerCardFooter)

export {
  PlayerCard,
  PlayerCardHeader,
  PlayerCardFooter,
  PlayerCardTitle,
  PlayerCardDescription,
  PlayerCardContent
}
