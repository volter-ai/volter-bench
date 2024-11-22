import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardHeaderProps extends React.ComponentProps<typeof CardHeader> {
  uid: string
}

interface PlayerCardTitleProps extends React.ComponentProps<typeof CardTitle> {
  uid: string
}

interface PlayerCardContentProps extends React.ComponentProps<typeof CardContent> {
  uid: string
}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardHeaderProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardTitleProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props}>
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

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCardContent = withClickable(PlayerCardContent)

export { 
  PlayerCard,
  PlayerCardHeader,
  PlayerCardTitle,
  PlayerCardContent
}
