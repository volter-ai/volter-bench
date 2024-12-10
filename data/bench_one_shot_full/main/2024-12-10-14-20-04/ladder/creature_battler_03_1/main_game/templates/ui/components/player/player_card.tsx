import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BasePlayerCardProps {
  uid: string
}

let PlayerCardHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof CardHeader> & BasePlayerCardProps
>(({ uid, ...props }, ref) => (
  <CardHeader ref={ref} uid={uid} {...props} />
))

let PlayerCardContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof CardContent> & BasePlayerCardProps
>(({ uid, ...props }, ref) => (
  <CardContent ref={ref} uid={uid} {...props} />
))

let PlayerCardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.ComponentProps<typeof CardTitle> & BasePlayerCardProps
>(({ uid, ...props }, ref) => (
  <CardTitle ref={ref} uid={uid} {...props} />
))

interface PlayerCardProps extends React.ComponentProps<typeof Card>, BasePlayerCardProps {
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
      <PlayerCardHeader uid={uid}>
        <PlayerCardTitle uid={uid}>{name}</PlayerCardTitle>
      </PlayerCardHeader>
      <PlayerCardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </PlayerCardContent>
    </Card>
  )
)

PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCard.displayName = "PlayerCard"

PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard, PlayerCardHeader, PlayerCardContent, PlayerCardTitle }
