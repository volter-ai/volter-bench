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

interface PlayerCardContentProps extends React.ComponentProps<typeof CardContent> {
  uid: string
}

interface PlayerCardHeaderProps extends React.ComponentProps<typeof CardHeader> {
  uid: string
}

interface PlayerCardTitleProps extends React.ComponentProps<typeof CardTitle> {
  uid: string
}

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardHeaderProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardTitleProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} {...props}>
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
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"

PlayerCard = withClickable(PlayerCard)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)

export { PlayerCard, PlayerCardContent, PlayerCardHeader, PlayerCardTitle }
