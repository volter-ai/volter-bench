import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle, CardContent as ShadcnCardContent } from "@/components/ui/card"

let PlayerCard = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { uid: string; playerName: string; imageUrl: string }
>(({ className, uid, playerName, imageUrl, ...props }, ref) => (
  <ShadcnCard ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
    <ShadcnCardHeader>
      <ShadcnCardTitle>{playerName}</ShadcnCardTitle>
    </ShadcnCardHeader>
    <ShadcnCardContent>
      <img src={imageUrl} alt={playerName} className="w-full h-48 object-cover rounded-md" />
    </ShadcnCardContent>
  </ShadcnCard>
))

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
