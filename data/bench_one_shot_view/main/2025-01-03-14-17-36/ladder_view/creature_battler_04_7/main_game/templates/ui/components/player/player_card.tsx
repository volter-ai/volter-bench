import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentPropsWithoutRef<typeof Card> {
  uid: string;
  playerName: string;
  playerImage: string;
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, playerName, playerImage, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
      <CardHeader>
        <CardTitle>{playerName}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={playerImage} alt={playerName} className="w-full h-auto" />
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
