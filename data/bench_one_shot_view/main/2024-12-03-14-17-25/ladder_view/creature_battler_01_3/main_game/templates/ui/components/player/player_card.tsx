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

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props}>
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

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardHeaderProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardTitleProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={cn("p-6 pt-0", className)} {...props} />
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

export { PlayerCard, PlayerCardHeader, PlayerCardTitle, PlayerCardContent }
