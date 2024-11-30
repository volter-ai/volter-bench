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
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <PlayerCardHeader uid={uid}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </PlayerCardHeader>
      <PlayerCardContent uid={uid}>
        <h3 className="text-lg font-semibold text-center">{name}</h3>
      </PlayerCardContent>
    </Card>
  )
)

let PlayerCardHeader = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} uid={uid} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} uid={uid} {...props} />
  )
)

PlayerCardRoot.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCardRoot = withClickable(PlayerCardRoot)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)

export { PlayerCardRoot as PlayerCard }
