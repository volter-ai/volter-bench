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

interface PlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCardRoot = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
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

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} uid={uid} {...props} />
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} uid={uid} {...props} />
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} uid={uid} {...props} />
)

PlayerCardRoot.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardTitle.displayName = "PlayerCardTitle"

PlayerCardRoot = withClickable(PlayerCardRoot)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardTitle = withClickable(PlayerCardTitle)

export { PlayerCardRoot as PlayerCard }
