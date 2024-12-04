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

interface BasePlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
}

interface PlayerCardProps extends BasePlayerCardProps {
  name: string
  imageUrl: string
}

let PlayerCardRoot = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props} />
  )
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <PlayerCardRoot ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
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
    </PlayerCardRoot>
  )
)

PlayerCardRoot.displayName = "PlayerCardRoot"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCard.displayName = "PlayerCard"

PlayerCardRoot = withClickable(PlayerCardRoot)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
