import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable.tsx"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  playerName: string
  playerImage: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ uid, playerName, playerImage, className, ...props }, ref) => (
    <Card ref={ref} className={className} {...props}>
      <CardHeader>
        <CardTitle>{playerName}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={playerImage} alt={`${playerName}'s image`} className="w-full h-auto" />
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
