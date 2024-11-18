import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCardBase = React.forwardRef<HTMLDivElement, PlayerCardProps>(
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

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} uid={uid} {...props} />
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} uid={uid} {...props} />
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} uid={uid} {...props} />
)

PlayerCardBase.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCardTitle.displayName = "PlayerCardTitle"

let PlayerCard = withClickable(PlayerCardBase)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCardTitle = withClickable(PlayerCardTitle)

export { PlayerCard }
