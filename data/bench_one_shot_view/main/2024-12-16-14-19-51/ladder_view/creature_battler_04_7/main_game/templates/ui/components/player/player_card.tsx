import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardHeaderProps extends React.ComponentProps<typeof CardHeader> {
  uid: string
}

interface PlayerCardContentProps extends React.ComponentProps<typeof CardContent> {
  uid: string
}

interface PlayerCardTitleProps extends React.ComponentProps<typeof CardTitle> {
  uid: string
}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardHeaderProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardTitleProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <PlayerCardHeader uid={`${uid}-header`}>
        <PlayerCardTitle uid={`${uid}-title`}>{name}</PlayerCardTitle>
      </PlayerCardHeader>
      <PlayerCardContent uid={`${uid}-content`}>
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
PlayerCardContent.displayName = "PlayerCardContent" 
PlayerCardTitle.displayName = "PlayerCardTitle"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardTitle = withClickable(PlayerCardTitle)

export { PlayerCard, PlayerCardHeader, PlayerCardContent, PlayerCardTitle }
