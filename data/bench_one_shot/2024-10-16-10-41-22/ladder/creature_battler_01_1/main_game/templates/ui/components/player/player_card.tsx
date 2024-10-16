import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
  CardContent as ShadcnCardContent,
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentPropsWithoutRef<typeof ShadcnCard> {
  uid: string;
  playerName: string;
  imageUrl: string;
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, playerName, imageUrl, ...props }, ref) => (
    <ShadcnCard ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <ShadcnCardHeader uid={`${uid}-header`}>
        <ShadcnCardTitle uid={`${uid}-title`}>{playerName}</ShadcnCardTitle>
      </ShadcnCardHeader>
      <ShadcnCardContent uid={`${uid}-content`}>
        <img src={imageUrl} alt={playerName} className="w-full h-48 object-cover rounded-md" />
      </ShadcnCardContent>
    </ShadcnCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
