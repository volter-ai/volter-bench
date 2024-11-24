import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CreatureCardRoot = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props} />
  )
)

let CreatureCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardRoot uid={`${uid}-root`} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="flex justify-between items-center">
              <span className="font-bold">HP:</span>
              <span>{hp}</span>
            </div>
          </div>
        </CreatureCardContent>
      </CreatureCardRoot>
    )
  }
)

CreatureCardRoot.displayName = "CreatureCardRoot"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCard.displayName = "CreatureCard"

CreatureCardRoot = withClickable(CreatureCardRoot)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
