import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentPropsWithoutRef<typeof Card> {
  uid: string;
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader>
        <CardTitle>{props.playerName}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={props.imageUrl} alt={props.playerName} className="w-full h-48 object-cover rounded-md" />
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
