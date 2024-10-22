import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

let PlayerCard = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof Card> & { uid: string; playerName: string; imageUrl: string }
>(({ className, uid, playerName, imageUrl, ...props }, ref) => (
  <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
    <CardHeader>
      <CardTitle>{playerName}</CardTitle>
    </CardHeader>
    <CardContent>
      <img src={imageUrl} alt={playerName} className="w-full h-auto" />
    </CardContent>
  </Card>
))

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
