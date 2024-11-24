import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props} />
  )
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

CustomCard.displayName = "CustomCard"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardTitle.displayName = "CustomCardTitle" 
CustomCardContent.displayName = "CustomCardContent"

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomCardContent = withClickable(CustomCardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, ...props }, ref) => {
    return (
      <CustomCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
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
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
