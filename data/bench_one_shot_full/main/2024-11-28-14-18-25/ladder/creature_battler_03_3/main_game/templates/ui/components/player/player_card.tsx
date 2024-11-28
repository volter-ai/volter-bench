import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface CardComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let PlayerCardBase = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} uid={uid} className={className} {...props} />
  )
)

let PlayerCardHeaderBase = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} uid={uid} className={className} {...props} />
  )
)

let PlayerCardContentBase = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} uid={uid} className={className} {...props} />
  )
)

PlayerCardBase = withClickable(PlayerCardBase)
PlayerCardHeaderBase = withClickable(PlayerCardHeaderBase)
PlayerCardContentBase = withClickable(PlayerCardContentBase)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => {
    return (
      <PlayerCardBase ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <PlayerCardHeaderBase uid={`${uid}-header`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-cover rounded-t-xl"
          />
        </PlayerCardHeaderBase>
        <PlayerCardContentBase uid={`${uid}-content`}>
          <h3 className="text-lg font-bold text-center">{name}</h3>
        </PlayerCardContentBase>
      </PlayerCardBase>
    )
  }
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
