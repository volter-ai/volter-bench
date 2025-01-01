import * as React from "react"
import { Card as ShadcnCard, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle, CardContent as ShadcnCardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable.tsx"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string;
  playerName: string;
  playerImage: string;
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(({ className, playerName, playerImage, uid, ...props }, ref) => (
  <ShadcnCard ref={ref} className={className} {...props}>
    <ShadcnCardHeader>
      <img src={playerImage} alt={`${playerName}'s image`} className="w-full h-auto rounded-t-xl" />
      <ShadcnCardTitle>{playerName}</ShadcnCardTitle>
    </ShadcnCardHeader>
    <ShadcnCardContent>
      {/* Additional content can be added here */}
    </ShadcnCardContent>
  </ShadcnCard>
))

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
