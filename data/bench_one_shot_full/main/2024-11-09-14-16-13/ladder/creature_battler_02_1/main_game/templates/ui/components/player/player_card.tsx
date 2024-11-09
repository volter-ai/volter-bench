import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"

interface BasePlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
}

interface PlayerCardProps extends BasePlayerCardProps {
  name: string
  imageUrl: string
}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} uid={uid} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} uid={uid} />
  )
)

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

PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCard.displayName = "PlayerCard"

PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard, PlayerCardHeader, PlayerCardContent }
