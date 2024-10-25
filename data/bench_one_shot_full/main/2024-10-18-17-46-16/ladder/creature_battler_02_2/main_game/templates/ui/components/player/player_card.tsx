import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

interface CardProps extends React.ComponentPropsWithoutRef<typeof ShadcnCard> {
  uid: string;
}

let Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

Card.displayName = "Card"
Card = withClickable(Card)

interface PlayerCardProps extends CardProps {
  playerName: string;
  imageUrl: string;
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, playerName, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader>
        <CardTitle>{playerName}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={imageUrl} alt={playerName} className="w-full h-48 object-cover rounded-md" />
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
