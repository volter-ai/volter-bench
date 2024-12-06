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

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface PlayerCardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <PlayerCardHeader uid={`${uid}-header`}>
        <CardTitle>{name}</CardTitle>
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
    <CardHeader ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardContentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} uid={uid} {...props} />
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)

export { PlayerCard }
