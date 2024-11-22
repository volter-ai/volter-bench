import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface PlayerCardSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCardRoot = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
      <PlayerCardHeader uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </PlayerCardHeader>
      <PlayerCardContent uid={`${uid}-content`}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </PlayerCardContent>
    </Card>
  )
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => (
    <CardHeader uid={uid} ref={ref} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => (
    <CardContent uid={uid} ref={ref} {...props} />
  )
)

PlayerCardRoot.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCardRoot = withClickable(PlayerCardRoot)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)

export { PlayerCardRoot as PlayerCard, PlayerCardHeader, PlayerCardContent }
