import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"

interface BasePlayerCardProps {
  uid: string
}

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement>, BasePlayerCardProps {
  name: string
  imageUrl: string
}

interface PlayerCardSubComponentProps extends React.HTMLAttributes<HTMLDivElement>, BasePlayerCardProps {}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let PlayerCardFooter = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardFooter ref={ref} {...props} />
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} {...props}>
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
      <PlayerCardFooter uid={uid} className="flex justify-between" />
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardFooter.displayName = "PlayerCardFooter"
PlayerCardTitle.displayName = "PlayerCardTitle"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardFooter = withClickable(PlayerCardFooter)
PlayerCardTitle = withClickable(PlayerCardTitle)

export { PlayerCard }
