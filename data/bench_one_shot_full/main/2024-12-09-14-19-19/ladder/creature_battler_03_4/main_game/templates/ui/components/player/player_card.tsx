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
    <Card ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
      <PlayerCardHeaderSection uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </PlayerCardHeaderSection>
      <PlayerCardContentSection uid={`${uid}-content`}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </PlayerCardContentSection>
    </Card>
  )
)

let PlayerCardHeaderSection = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => (
    <CardHeader ref={ref} uid={uid} {...props} />
  )
)

let PlayerCardContentSection = React.forwardRef<HTMLDivElement, PlayerCardSubComponentProps>(
  ({ uid, ...props }, ref) => (
    <CardContent ref={ref} uid={uid} {...props} />
  )
)

PlayerCardRoot.displayName = "PlayerCard"
PlayerCardHeaderSection.displayName = "PlayerCardHeader"
PlayerCardContentSection.displayName = "PlayerCardContent"

PlayerCardRoot = withClickable(PlayerCardRoot)
PlayerCardHeaderSection = withClickable(PlayerCardHeaderSection)
PlayerCardContentSection = withClickable(PlayerCardContentSection)

export { PlayerCardRoot as PlayerCard }
