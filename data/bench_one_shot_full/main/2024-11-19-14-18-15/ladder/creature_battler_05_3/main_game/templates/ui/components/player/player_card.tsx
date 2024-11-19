import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} uid={uid} className={cn("", className)} {...props} />
  )
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & {uid: string}>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} uid={uid} className={cn("", className)} {...props} />
  )
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
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

PlayerCard.displayName = "PlayerCard"
PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardContent.displayName = "PlayerCardContent"

PlayerCard = withClickable(PlayerCard)
PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardContent = withClickable(PlayerCardContent)

export { PlayerCard, PlayerCardHeader, PlayerCardContent }
